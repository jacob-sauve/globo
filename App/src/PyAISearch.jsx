import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'



// spawn a Python child process
const { spawn } = require('child_process');
const resultsPath = "frontend/results.csv"

function queryAISearchBot(prompt, budget, origin_airport) {
    // call has first arg scriptpath, then function arguments
    const searchBot = spawn(
        'python',
        [
            "backend/ai_search.py",
            "client=client",
            `prompt=${prompt}`,
            `budget=${budget}`,
            `origin_airport=${origin_airport}`
            ]
        );

    searchBot.stdout.on('data', (data) => {
        console.log(`ai_search.py output: ${data}`);
    });

    searchBot.stderr.on('data', (data) => {
        console.error(`ai_search.py error: ${data}`);
        return resultsPath;
    });

    searchBot.on('close', (code) => {
        console.log(`ai_search.py exited with code ${code}`);
        return resultsPath;
    });

    }

export queryAISearchBot;