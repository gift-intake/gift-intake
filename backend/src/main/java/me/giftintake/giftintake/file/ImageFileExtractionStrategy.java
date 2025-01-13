package me.giftintake.giftintake.file;

import net.sourceforge.tess4j.Tesseract;
import org.springframework.lang.NonNull;
import org.springframework.stereotype.Component;

import java.io.File;

@Component
public class ImageFileExtractionStrategy implements FileExtractionStrategy {

    @Override
    public @NonNull String extractText(@NonNull File file) {
      
        Tesseract tesseract = new Tesseract();
        try {
            return tesseract.doOCR(file);
        } catch (Exception e) {
            throw new RuntimeException("Failed to extract text from image", e);
        }
    }

}
