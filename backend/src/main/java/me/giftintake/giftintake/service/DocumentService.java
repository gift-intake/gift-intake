package me.giftintake.giftintake.service;

import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;
import me.giftintake.giftintake.file.FileExtractionStrategy;
import me.giftintake.giftintake.file.FileExtractionStrategyFactory;
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
  private final FileExtractionStrategyFactory factory;

  @Autowired
  public DocumentService(FileExtractionStrategyFactory factory) {
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

    ArrayList<FileExtractionRecord> attachments = new ArrayList<>();

    try (InputStream inputStream = file.getInputStream()) {
      Path emailTempFile = Files.createTempFile(file.getName().replaceAll(FILE_REGEX, "_"),
          ".msg");
      Files.write(emailTempFile, file.getBytes());
      emailTempFile.toFile().deleteOnExit();

      attachments.add(new FileExtractionRecord(
          file.getOriginalFilename(),
          ".msg",
          emailTempFile
      ));

      MAPIMessage message = new MAPIMessage(inputStream);

      for (AttachmentChunks attachment : message.getAttachmentFiles()) {
        String attachmentName = attachment.getAttachFileName().getValue();
        String extension = attachment.getAttachExtension().getValue();

        Path tempFile = Files.createTempFile(
            attachmentName.replaceAll(FILE_REGEX, "_"),
            extension
        );
        System.out.println("Created temp file: " + tempFile);
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
