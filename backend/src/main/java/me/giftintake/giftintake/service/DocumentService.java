package me.giftintake.giftintake.service;

import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import me.giftintake.giftintake.file.TextExtractionStrategyFactory;
import me.giftintake.giftintake.model.FileExtractionRecord;
import me.giftintake.giftintake.model.OutlookEmail;
import org.apache.poi.hsmf.MAPIMessage;
import org.apache.poi.hsmf.datatypes.AttachmentChunks;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.lang.NonNull;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

@Service
public final class DocumentService {

  private static final String FILE_REGEX = "[^a-zA-Z0-9.-]";
  private final TextExtractionStrategyFactory factory;

  @Autowired
  public DocumentService(TextExtractionStrategyFactory factory) {
    this.factory = factory;
  }

  /**
   * Saves the incoming email file and attachments to a temporary location and returns a list of
   * {@link FileExtractionRecord} objects.
   *
   * @param file The email file to be processed
   * @return A list of {@link FileExtractionRecord} objects representing the files to be processed.
   */
  public List<FileExtractionRecord> uploadDocument(@NonNull MultipartFile file) {
    if (file.isEmpty()) {
      throw new IllegalArgumentException("File is empty");
    }

    var attachments = new ArrayList<FileExtractionRecord>();

    try (var inputStream = file.getInputStream()) {
      var emailTempFile = Files.createTempFile(file.getName().replaceAll(FILE_REGEX, "_"),
          ".msg");
      Files.write(emailTempFile, file.getBytes());
      emailTempFile.toFile().deleteOnExit();

      attachments.add(new FileExtractionRecord(
          file.getOriginalFilename(),
          ".msg",
          emailTempFile
      ));

      var message = new MAPIMessage(inputStream);

      for (var attachment : message.getAttachmentFiles()) {
        var attachmentName = attachment.getAttachFileName().getValue();
        var extension = attachment.getAttachExtension().getValue();

        var tempFile = Files.createTempFile(
            attachmentName.replaceAll(FILE_REGEX, "_"),
            extension
        );
        tempFile.toFile().deleteOnExit();

        Files.write(tempFile, attachment.getAttachData().getValue());
        attachments.add(new FileExtractionRecord(
            attachmentName,
            extension,
            tempFile
        ));
      }

      return attachments;
    } catch (Exception e) {
      throw new RuntimeException("Failed to process document", e);
    }
  }

  /**
   * Extracts the text from the email file and attachments.
   *
   * @param records The list of {@link FileExtractionRecord} objects representing the files to be
   *                processed.
   * @return An {@link OutlookEmail} object representing the email and attachments.
   */
  public @NonNull OutlookEmail extractText(@NonNull List<FileExtractionRecord> records) {
    var attachments = records
        .stream()
        .filter(fileExtractionRecord -> !fileExtractionRecord.extension().equals(".msg"))
        .map(fileExtractionRecord -> {
          var extractor = factory.getStrategy(fileExtractionRecord.extension());
          var extractedText = extractor.extractText(fileExtractionRecord.file().toFile());
          fileExtractionRecord.file().toFile().delete();
          return new OutlookEmail.Attachment(
              fileExtractionRecord.name(),
              fileExtractionRecord.extension(),
              extractedText
          );
        }).toList();
    return records
        .stream()
        .filter(fileExtractionRecord -> fileExtractionRecord.extension().equals(".msg"))
        .findFirst()
        .map(fileExtractionRecord -> {
          var extractor = factory.getStrategy(fileExtractionRecord.extension());
          var extractedText = extractor.extractText(fileExtractionRecord.file().toFile());
          fileExtractionRecord.file().toFile().delete();
          return new OutlookEmail(extractedText, attachments);
        })
        .orElseThrow(() -> new IllegalArgumentException("No email file found"));
  }
}
