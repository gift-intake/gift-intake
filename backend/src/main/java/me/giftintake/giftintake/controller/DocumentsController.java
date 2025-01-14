package me.giftintake.giftintake.controller;

import java.util.UUID;
import me.giftintake.giftintake.file.FileExtractionStrategyFactory;
import me.giftintake.giftintake.service.DocumentService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

/**
 * Handles the requests for uploading documents to be processed.
 */
@RestController
@RequestMapping("/api/documents")
public final class DocumentsController {

  private final DocumentService documentService;
  private final FileExtractionStrategyFactory factory;

  @Autowired
  public DocumentsController(DocumentService documentService,
      FileExtractionStrategyFactory factory) {
    this.documentService = documentService;
    this.factory = factory;
  }

  /**
   * Uploads a document to the server to be processed
   *
   * @param file the document to upload
   * @return a response entity
   */
  @PostMapping
  public ResponseEntity<Void> uploadDocument(@RequestParam("file") MultipartFile file) {
    var results = documentService.uploadDocument(file);

    var email = documentService.extractText(results);
    System.out.println(email);

    return ResponseEntity.ok().build();
  }

  /**
   * Gets the status of a document
   *
   * @param id the id of the document
   * @return a response entity
   */
  @GetMapping("/status")
  public ResponseEntity<Void> documentStatus(@RequestParam("id") UUID id) {
    return ResponseEntity.ok().build();
  }

  /**
   * Gets the result of a document
   *
   * @param id the id of the document
   * @return a response entity
   */
  @GetMapping("/result")
  public ResponseEntity<Void> documentResult(@RequestParam("id") UUID id) {
    return ResponseEntity.ok().build();
  }
}
