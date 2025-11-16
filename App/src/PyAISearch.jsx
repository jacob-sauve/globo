import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'



// spawn a Python child process
const { spawn } = require('child_process');

function queryAISearchBot() {
    // call has first arg scriptpath, then function arguments
    const searchBot = spawn('python', ["../../backend/ai_search.py", ]);


    }