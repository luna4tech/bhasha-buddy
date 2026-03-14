import {
    Streamlit,
    withStreamlitConnection,
    ComponentProps,
} from "streamlit-component-lib"
import React, { useEffect, useState, ReactElement, useRef } from "react"
import "./styles.css"

function PracticeComponent({ args, theme }: ComponentProps): ReactElement {
    const { storyTextWords } = args;
    const { currentSpeakingWordIndex } = args;
    const { storyTitle } = args;
    const { wordsAudio } = args;
    const [currentWordIndex, setCurrentWordIndex] = useState(-1);

    const audioRef = useRef<HTMLAudioElement | null>(null);

    useEffect(() => {
        Streamlit.setFrameHeight()
    }, [theme, storyTextWords]);

    const CLEAN_WORD = (word: string) => {
        return word.toLowerCase().replace(/^[!"#$%&'()*+,\-./:;<=>?@[\]^_`{|}~]+|[!"#$%&'()*+,\-./:;<=>?@[\]^_`{|}~]+$/g, ""); // this is the same punctuation list from python's string.punctuation
    };

    const speakWord = (word: any, index: any) => {
        const mainAudio = audioRef.current;
        mainAudio?.pause();

        setCurrentWordIndex(index);
        console.log('Speaking word:', word['text']);
        const audio = new Audio(wordsAudio[CLEAN_WORD(word['text'])])
        audio.play().catch((error) => console.error('Error playing audio:', error));
    };

    return (
        <div>
            <h3>{storyTitle}</h3>
            <div className="scrollable-content">
            {storyTextWords.map((word: any, index: any) => (
                <span
                    key={index}
                    className={index === currentWordIndex ? "word highlight" : (index === currentSpeakingWordIndex ? "word speaking" : "word no-highlight")}
                    onClick={() => speakWord(word, index)}
                >
                    {word['text']}
                </span>
                ))}
            </div>
        </div>
    )
}

export default withStreamlitConnection(PracticeComponent)