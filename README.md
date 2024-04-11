# Fake_Job_detecting_BERT


              precision    recall  f1-score   support

         0.0       0.99      0.99      0.99      3414
         1.0       0.81      0.74      0.77       162

    accuracy                           0.98      3576
   macro avg       0.90      0.87      0.88      3576
weighted avg       0.98      0.98      0.98      3576


The test dataset report shows similar trends to the validation dataset report after undersampling. The F1-score for the fraudulent class has increased to 0.77 from 0.74 before undersampling, indicating that undersampling has helped in improving the model's ability to correctly identify fraudulent transactions.
