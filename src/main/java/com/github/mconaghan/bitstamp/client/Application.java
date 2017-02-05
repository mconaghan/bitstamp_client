package com.github.mconaghan.bitstamp.client;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
@SuppressWarnings("checkstyle:hideutilityclassconstructor")
public class Application {

    public static void main(final String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
