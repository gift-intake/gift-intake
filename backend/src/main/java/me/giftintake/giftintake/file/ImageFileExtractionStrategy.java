package me.giftintake.giftintake.file;

import net.sourceforge.tess4j.Tesseract;

import java.io.File;

public class ImageFileExtractionStrategy implements FileExtractionStrategy {

    @Override
    public String extractText(File file) {
        Tesseract tesseract = new Tesseract();
        try {
            return tesseract.doOCR(file);
        } catch (Exception e) {
            throw new RuntimeException("Failed to extract text from image", e);
        }
    }

}
