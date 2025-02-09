import {
    Streamlit,
    withStreamlitConnection,
    ComponentProps,
} from "streamlit-component-lib"
import React, { useEffect, useState, ReactElement, useRef } from "react"
import "./styles.css"

function ReadingComponent({ args, theme }: ComponentProps): ReactElement {
    const { audio_src } = args;
    const { words } = args;
    const { storyTitle } = args;
    const { language } = args;
    const [currentWordIndex, setCurrentWordIndex] = useState(-1);

    const audioRef = useRef<HTMLAudioElement | null>(null);

    useEffect(() => {
        Streamlit.setFrameHeight()
    }, [theme, words]);

    const speakWord = (word: any, index: any) => {
        if ("speechSynthesis" in window) {
            var playbackSpeed = 1.0;
            const audio = audioRef.current;
            if(audio) {
                playbackSpeed = audio.playbackRate;
            }
            const utterance = new SpeechSynthesisUtterance(word);
            utterance.rate = playbackSpeed;
            utterance.lang = language;
            setCurrentWordIndex(index);
            speechSynthesis.speak(utterance);
        } else {
            alert("Speech synthesis not supported in this browser.");
        }
    };

    useEffect(() => {
        const audio = audioRef.current;
        if(!audio) {
            return;
        }
        const handleTimeUpdate = () => {
            const currentTime = audio.currentTime;
            const wordCount = words.length;
            const timePerWord = audio.duration / wordCount;
            const newIndex = Math.floor(currentTime / timePerWord);

            const clampedIndex = Math.min(newIndex, wordCount - 1);
            setCurrentWordIndex(clampedIndex);
        };

        audio.addEventListener("timeupdate", handleTimeUpdate);

        return () => {
            audio.removeEventListener("timeupdate", handleTimeUpdate);
        };

    }, [words.length]);

    return (
        <div>
            <h3>{storyTitle}</h3>
            <div className="scrollable-content">
            {words.map((word: any, index: any) => (
                <span
                    key={index}
                    className={index === currentWordIndex ? "word highlight" : "word no-highlight"}
                    onClick={() => speakWord(word, index)}
                >
                    {word}
                </span>
                ))}
            </div>

            <div className="audio-wrapper">
                <audio ref={audioRef} controls className="audio-player">
                    <source src={audio_src} type="audio/mp3" />
                    Your browser does not support the audio element.
                </audio>
            </div>
        </div>
    )
}

export default withStreamlitConnection(ReadingComponent)