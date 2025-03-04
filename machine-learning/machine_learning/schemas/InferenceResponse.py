from pydantic import BaseModel, Field
from typing import Optional, Union, Literal


class EntityWithConfidence(BaseModel):
    """Base class for any entity that includes a confidence score"""

    entity: Optional[str] = None
    value: str
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)


class DonorInfo(BaseModel):
    """General donor information"""

    first_name: Optional[EntityWithConfidence] = None
    last_name: Optional[EntityWithConfidence] = None
    constituent_id: Optional[EntityWithConfidence] = None
    organization_name: Optional[EntityWithConfidence] = None


class ContactInfo(BaseModel):
    """Donor contact information"""

    email: Optional[EntityWithConfidence] = None
    phone: Optional[EntityWithConfidence] = None
    address: Optional[EntityWithConfidence] = None
    postal_code: Optional[EntityWithConfidence] = None
    city: Optional[EntityWithConfidence] = None
    province: Optional[EntityWithConfidence] = None


class GiftInfo(BaseModel):
    """Information about a donation"""

    type: str  # Base type field that will be overridden in subclasses
    payment_method: Optional[EntityWithConfidence] = None
    fundraiser_first_name: Optional[EntityWithConfidence] = None
    fundraiser_last_name: Optional[EntityWithConfidence] = None
    fundraiser_email: Optional[EntityWithConfidence] = None
    fundraiser_currency: Optional[EntityWithConfidence] = None


class Pledge(GiftInfo):
    """Information about a pledge"""

    type: Literal["pledge"] = "pledge"
    inital_payment_date: Optional[EntityWithConfidence] = None
    installments: Optional[EntityWithConfidence] = None
    installment_frequency: Optional[EntityWithConfidence] = None
    pledge_amount: Optional[EntityWithConfidence] = None


class PledgePayment(GiftInfo):
    """Information about a pledge payment"""

    type: Literal["pledge_payment"] = "pledge_payment"
    payment_date: Optional[EntityWithConfidence] = None
    payment_amount: Optional[EntityWithConfidence] = None


class RecurringGift(GiftInfo):
    """Recurring gift setup"""

    type: Literal["recurring_gift"] = "recurring_gift"
    installment_frequency: Optional[EntityWithConfidence] = None
    initial_payment_date: Optional[EntityWithConfidence] = None
    gift_date: Optional[EntityWithConfidence] = None


class RecurringGiftPayment(GiftInfo):
    """Payment against a recurring gift"""

    type: Literal["recurring_gift_payment"] = "recurring_gift_payment"
    payment_date: Optional[EntityWithConfidence] = None


class Gift(GiftInfo):
    """Information about a gift"""

    type: Literal["one_time_gift"] = "one_time_gift"
    gift_date: Optional[EntityWithConfidence] = None


GiftType = Union[Pledge, PledgePayment, RecurringGift, RecurringGiftPayment, Gift]


class SummaryResponse(BaseModel):
    """Model for summarization response"""
    summary: str


class InferenceResponse(BaseModel):
    """Complete inference response model"""

    summary: Optional[str] = None
    donor_info: Optional[DonorInfo] = None
    contact_info: Optional[ContactInfo] = None
    gift_info: Optional[GiftType] = None
