package me.giftintake.giftintake.model;

import java.nio.file.Path;

public record FileExtractionRecord(String name, String extension, Path file) {

}
