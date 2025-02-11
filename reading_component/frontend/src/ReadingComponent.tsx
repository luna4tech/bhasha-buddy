import {
    Streamlit,
    withStreamlitConnection,
    ComponentProps,
} from "streamlit-component-lib"
import React, { useEffect, useState, ReactElement, useRef } from "react"
import "./styles.css"

function ReadingComponent({ args, theme }: ComponentProps): ReactElement {
    const { audioSrc } = args;
    const { storyText } = args;
    const { wordsMetadata } = args;
    const { storyTitle } = args;
    const { wordsAudio } = args;
    const [currentWordIndex, setCurrentWordIndex] = useState(-1);

    const audioRef = useRef<HTMLAudioElement | null>(null);

    useEffect(() => {
        Streamlit.setFrameHeight()
    }, [theme, wordsMetadata]);

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

    useEffect(() => {
        const audio = audioRef.current;
        if(!audio) {
            return;
        }
        const handleTimeUpdate = () => {
            const currentTime = audio.currentTime;
            // find currentTime in the wordsMetadata array
            for (let i = 0; i < wordsMetadata.length; i++) {
                if (currentTime >= wordsMetadata[i]['start'] && currentTime <= wordsMetadata[i]['end']) {
                    setCurrentWordIndex(i);
                    return;
                }
            }
            // const wordCount = wordsMetadata.length;
            // const timePerWord = audio.duration / wordCount;
            // const newIndex = Math.floor(currentTime / timePerWord);

            // const clampedIndex = Math.min(newIndex, wordCount - 1);
            // setCurrentWordIndex(clampedIndex);
        };

        audio.addEventListener("timeupdate", handleTimeUpdate);

        return () => {
            audio.removeEventListener("timeupdate", handleTimeUpdate);
        };

    }, [wordsMetadata.length]);

    return (
        <div>
            <h3>{storyTitle}</h3>
            <div className="scrollable-content">
            {wordsMetadata.map((word: any, index: any) => (
                <span
                    key={index}
                    className={index === currentWordIndex ? "word highlight" : "word no-highlight"}
                    onClick={() => speakWord(word, index)}
                >
                    {word['text']}
                </span>
                ))}
            </div>

            <div className="audio-wrapper">
                <audio ref={audioRef} controls className="audio-player">
                    <source src={audioSrc} type="audio/mp3" />
                    Your browser does not support the audio element.
                </audio>
            </div>
        </div>
    )
}

export default withStreamlitConnection(ReadingComponent)