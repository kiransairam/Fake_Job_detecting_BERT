# Fake_Job_detecting_BERT


              precision    recall  f1-score   support

         0.0       0.99      0.99      0.99      3414
         1.0       0.81      0.74      0.77       162

    accuracy                           0.98      3576
   macro avg       0.90      0.87      0.88      3576
weighted avg       0.98      0.98      0.98      3576


The test dataset report shows similar trends to the validation dataset report after undersampling. The F1-score for the fraudulent class has increased to 0.77 from 0.74 before undersampling, indicating that undersampling has helped in improving the model's ability to correctly identify fraudulent transactions.

The classification report provides more detailed performance metrics for the model, including precision, recall, and F1-score for both classes (fraudulent and non-fraudulent) as well as overall accuracy, macro-averaged F1-score, and weighted-averaged F1-score.

Overall, the model appears to perform well on the non-fraudulent class (high precision, recall, and F1-score), but less well on the fraudulent class (lower precision, recall, and F1-score). This suggests that the model may need further tuning or refinement in order to better detect fraudulent transactions.
