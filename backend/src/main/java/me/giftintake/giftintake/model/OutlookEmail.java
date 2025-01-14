package me.giftintake.giftintake.model;

import java.util.List;

/**
 * Represents an email and its attachments in text form.
 */
public record OutlookEmail(String body, List<Attachment> attachments) {

  /**
   * Represents an attachment to an email.
   */
  public record Attachment(String name, String extension, String content) {

  }
}
