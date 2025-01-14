package me.giftintake.giftintake.file;

import java.io.File;
import java.io.IOException;
import org.apache.poi.hsmf.MAPIMessage;
import org.apache.poi.hsmf.exceptions.ChunkNotFoundException;
import org.springframework.lang.NonNull;
import org.springframework.stereotype.Component;

/**
 * Uses the Apache POI library to extract text from an Outlook email file.
 */
@Component
public class OutlookTextExtractionStrategy implements TextExtractionStrategy {

  @Override
  public @NonNull String extractText(@NonNull File file) {
    try (var message = new MAPIMessage(file)) {
      var body = message.getTextBody();

      if (body == null || body.isEmpty()) {
        body = message.getHtmlBody();
      }

      return body;
    } catch (IOException | ChunkNotFoundException e) {
      throw new RuntimeException(e);
    }
  }
}
