# Alert Text Detector 🚨📱
![ss](Images/ss_(1).png)
## Project Overview

Alert Text Detector is an advanced Natural Language Processing (NLP) model designed to identify and flag emergency or critical alert messages across social media platforms. Leveraging state-of-the-art machine learning techniques, this project aims to provide real-time detection of urgent communications.

## Key Features

- 🧠 **Advanced NLP Model**: Utilizes Bertweet Base model for sophisticated text classification
- 🔍 **High Precision Detection**: Achieves over 93% precision in identifying alert texts
- 📍 **Location-Based Alerts**: Customizable alert distribution based on user interests and locations
- 🔬 **Comprehensive Preprocessing**: Includes lemmatization, keyword extraction, and hashtag analysis

## Performance Metrics

### Validation Results
- **Accuracy**: 91.07%
- **Precision**: 89.46%
- **Recall**: 91.05%
- **F1 Score**: 90.25%

### Test Dataset Results
- **Accuracy**: 96.37%
- **Precision**: 93.17%
- **Recall**: 99.83%
- **F1 Score**: 96.39%

## Technology Stack

- **Machine Learning**: Hugging Face Transformers, Bertweet Base Model
- **Data Processing**: Pandas, NumPy, NLTK
- **Model Training**: PyTorch
- **Web Framework**: Flask
- **Database**: SQLite3


## Installation

1. Clone the repository
```bash
git clone https://github.com/saivasanthg/Alert_Text_Detector.git
cd Alert_Text_Detector

```



## Data Preprocessing Techniques

- Lemmatization
- Keyword extraction using `paraphrase-MiniLM-L6-v2`
- Hashtag analysis
- Train-test split (80% training, 20% validation)

  TRAINING PROCESS
![ss](Images/Screenshot_6.png)


![ss](Images/Screenshot_7.png)


## Future Roadmap

- [ ] Multi-language support
- [ ] Real-time streaming alert detection
- [ ] Integration with more social media platforms
- [ ] Decoding of emoticons for better contextual understanding


## License

Distributed under the Apache 2.0 License. See `LICENSE` for more information.

## Contact

Sai Vasanth G
gsvsanth2004@gmail.com

