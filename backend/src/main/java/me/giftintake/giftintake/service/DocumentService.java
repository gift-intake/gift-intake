package me.giftintake.giftintake.service;

import org.apache.poi.hsmf.MAPIMessage;
import org.springframework.lang.NonNull;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

@Service
public final class DocumentService {

    public void uploadDocument(@NonNull MultipartFile file) {
        if (file.isEmpty()) {
            throw new IllegalArgumentException("File is empty");
        }

        try(var inputStream = file.getInputStream()) {
            MAPIMessage message = new MAPIMessage(inputStream);

            String body = message.getTextBody();

            if (body == null || body.isEmpty()) {
                body = message.getHtmlBody();
            }
        } catch (Exception e) {
            throw new RuntimeException("Failed to process document", e);
        }
    }
}
