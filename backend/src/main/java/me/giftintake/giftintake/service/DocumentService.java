package me.giftintake.giftintake.service;

import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
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

  public List<FileExtractionRecord> uploadDocument(@NonNull MultipartFile file) {
    if (file.isEmpty()) {
      throw new IllegalArgumentException("File is empty");
    }

    ArrayList<FileExtractionRecord> attachments = new ArrayList<>();

    try (InputStream inputStream = file.getInputStream()) {
      Path emailTempFile = Files.createTempFile(file.getName().replaceAll(FILE_REGEX, "_"),
          ".msg");
      emailTempFile.toFile().deleteOnExit();

      attachments.add(new FileExtractionRecord(
          file.getOriginalFilename(),
          file.getOriginalFilename().substring(file.getOriginalFilename().lastIndexOf(".") + 1),
          emailTempFile
      ));

      MAPIMessage message = new MAPIMessage(inputStream);

      for (AttachmentChunks attachment : message.getAttachmentFiles()) {
        String attachmentName = attachment.getAttachFileName().getValue();
        String extension = attachment.getAttachExtension().getValue();

        Path tempFile = Files.createTempFile(
            attachmentName.replaceAll(FILE_REGEX, "_"),
            ".tmp"
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


  public @NonNull List<FileExtractionRecord> extractText(@NonNull OutlookEmail email) {
    return List.of();
  }
}
