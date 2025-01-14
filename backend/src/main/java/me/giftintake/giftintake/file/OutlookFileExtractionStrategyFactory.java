package me.giftintake.giftintake.file;

import java.io.File;
import java.io.IOException;
import org.apache.poi.hsmf.MAPIMessage;
import org.apache.poi.hsmf.exceptions.ChunkNotFoundException;
import org.springframework.lang.NonNull;
import org.springframework.stereotype.Component;

@Component
public class OutlookFileExtractionStrategyFactory implements FileExtractionStrategy {

  @Override
  public @NonNull String extractText(@NonNull File file) {
    try (MAPIMessage message = new MAPIMessage(file)) {
      String body = message.getTextBody();

      if (body == null || body.isEmpty()) {
        body = message.getHtmlBody();
      }

      return body;
    } catch (IOException | ChunkNotFoundException e) {
      throw new RuntimeException(e);
    }
  }
}
