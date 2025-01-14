package me.giftintake.giftintake.model;

import java.nio.file.Path;

/**
 * Represents a file in the temporary directory that is to be extracted.
 */
public record FileExtractionRecord(String name, String extension, Path file) {

}
