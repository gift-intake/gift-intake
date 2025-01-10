package me.giftintake.giftintake.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.util.UUID;

/**
 * Handles the requests for uploading documents to be processed.
 */
@RestController
@RequestMapping("/api/documents")
public final class DocumentsController {

    /**
     * Uploads a document to the server to be processed
     * @param file the document to upload
     * @return a response entity
     */
    @PostMapping
    public ResponseEntity<Void> uploadDocument(@RequestParam("file") MultipartFile file) {
        return ResponseEntity.ok().build();
    }

    /**
     * Gets the status of a document
     * @param id the id of the document
     * @return a response entity
     */
    @GetMapping("/status")
    public ResponseEntity<Void> documentStatus(@RequestParam("id") UUID id) {
        return ResponseEntity.ok().build();
    }

    /**
     * Gets the result of a document
     * @param id the id of the document
     * @return a response entity
     */
    @GetMapping("/result")
    public ResponseEntity<Void> documentResult(@RequestParam("id") UUID id) {
        return ResponseEntity.ok().build();
    }
}
