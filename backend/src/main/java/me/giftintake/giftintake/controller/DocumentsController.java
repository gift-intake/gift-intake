package me.giftintake.giftintake.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

/**
 * Handles the requests for
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

}
