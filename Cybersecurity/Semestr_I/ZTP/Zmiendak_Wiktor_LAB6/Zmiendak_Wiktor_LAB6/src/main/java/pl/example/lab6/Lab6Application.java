package pl.example.lab6;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

import java.time.Clock;

@SpringBootApplication
public class Lab6Application {

    public static void main(String[] args) {
        SpringApplication.run(Lab6Application.class, args);
    }

    @Bean
    Clock clock() {
        return Clock.systemUTC();
    }
}
