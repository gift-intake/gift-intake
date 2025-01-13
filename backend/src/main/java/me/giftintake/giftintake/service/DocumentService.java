package me.giftintake.giftintake.service;

import me.giftintake.giftintake.model.OutlookEmail;
import org.apache.poi.hsmf.MAPIMessage;
import org.apache.poi.hsmf.datatypes.AttachmentChunks;
import org.springframework.lang.NonNull;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;

@Service
public final class DocumentService {
    private static final String FILE_REGEX = "[^a-zA-Z0-9.-]";

    public OutlookEmail uploadDocument(@NonNull MultipartFile file) {
        if (file.isEmpty()) {
            throw new IllegalArgumentException("File is empty");
        }

        try (var inputStream = file.getInputStream()) {
            MAPIMessage message = new MAPIMessage(inputStream);

            String body = message.getTextBody();

            if (body == null || body.isEmpty()) {
                body = message.getHtmlBody();
            }

            ArrayList<Path> attachments = new ArrayList<>();

            for (AttachmentChunks attachment : message.getAttachmentFiles()) {
                String attachmentName = attachment.getAttachFileName().getValue();

                Path tempFile = Files.createTempFile(
                        attachmentName.replaceAll(FILE_REGEX, "_"),
                        ".tmp"
                );

                tempFile.toFile().deleteOnExit();

                Files.write(tempFile, attachment.getAttachData().getValue());
                attachments.add(tempFile);
            }

            return new OutlookEmail(body, attachments);
        } catch (Exception e) {
            throw new RuntimeException("Failed to process document", e);
        }
    }

}
