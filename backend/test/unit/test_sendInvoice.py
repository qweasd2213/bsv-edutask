# from unittest.mock import patch
# from src.util.mocking_patching.invoice_mailer import InvoiceMailer

# def test_sebd_invoice_true():
#     #arrange
#     with patch("src.unit.mocking_patching.invoice_mailer.EmailClient") as MockEmailClient:
#         mock_client = MockEmailClient.return_value
#         mock_client.send.return_value = True



#         invoice_mailer = InvoiceMailer()
#         #act
#         result = invoice_mailer.send_invoice("test@email.com", 5000)
#         #assert
#         assert result is True