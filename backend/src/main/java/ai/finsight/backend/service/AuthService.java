package ai.finsight.backend.service;

import ai.finsight.backend.dto.request.LoginRequest;
import ai.finsight.backend.dto.request.RegisterRequest;
import ai.finsight.backend.dto.response.AuthResponse;
import ai.finsight.backend.exception.ApiException;
import ai.finsight.backend.model.User;
import ai.finsight.backend.repository.UserRepository;
import ai.finsight.backend.util.JwtUtil;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
@Slf4j
public class AuthService {
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtUtil jwtUtil;

    public AuthResponse register(RegisterRequest request) {
        log.info("Registering new user with email: {}", request.getEmail());
        if (userRepository.existsByEmail(request.getEmail())) {
            log.warn("Registration attempt with already registered email: {}", request.getEmail());
            throw ApiException.conflict("Email already registered", "EMAIL_ALREADY_REGISTERED");
        }

        User user = User.builder()
                .email(request.getEmail())
                .passwordHash(passwordEncoder.encode(request.getPassword()))
                .build();

        User saved = userRepository.save(user);
        log.info("User registered successfully with ID: {}", saved.getId());

        String token = jwtUtil.generateToken(saved.getEmail(), saved.getId());
        return AuthResponse.builder()
                .token(token)
                .userId(saved.getId())
                .email(saved.getEmail())
                .message("Registration successful")
                .build();
    }

    public AuthResponse login(LoginRequest request) {
        log.info("Login attempt for email: {}", request.getEmail());
        User user = userRepository.findByEmail(request.getEmail())
                .orElseThrow(() -> {
                    log.warn("Login attempt with non-existent email: {}", request.getEmail());
                    return ApiException.unauthorized("Invalid email or password", "INVALID_CREDENTIALS");
                });

        if (!passwordEncoder.matches(request.getPassword(), user.getPasswordHash())) {
            log.warn("Login attempt with invalid password for email: {}", request.getEmail());
            throw ApiException.unauthorized("Invalid email or password", "INVALID_CREDENTIALS");
        }

        log.info("User logged in successfully: {}", user.getEmail());
        String token = jwtUtil.generateToken(user.getEmail(), user.getId());

        return AuthResponse.builder()
                .token(token)
                .userId(user.getId())
                .email(user.getEmail())
                .message("Login successful")
                .build();
    }

}
