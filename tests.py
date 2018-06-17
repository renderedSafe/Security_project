import email_reading
import cv2

scraper = email_reading.EmailScraper()

email = scraper.get_newest_message(subject='Unique test subject text')


cv2.imshow('image', email.get_image_object())
cv2.waitKey()
