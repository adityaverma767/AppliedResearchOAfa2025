# Emotion-Driven Code Review Assistant

## What it Does
This tool looks at the comments and commit messages in your code to figure out how you're feeling.
Then it gives you personalized feedback based on those emotions to help you improve.

## How to Run It

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Reviewer**:
    You can run the `emotion_code_reviewer.py` script in a few ways:

    *   **With a demo**:
        ```bash
        python emotion_code_reviewer.py --demo
        ```

    *   **With a specific file**:
        ```bash
        python emotion_code_reviewer.py --file your_code.py --commit "Your commit message here" --name "Your Name"
        ```
        Replace `your_code.py` with the path to your Python file, and optionally provide a commit message and developer name.

    *   **Interactive Mode** (uncomment `interactive_mode()` in `emotion_code_reviewer.py` to enable):
        ```bash
        python emotion_code_reviewer.py
        ```
        Then, you can type city names to get weather information.
