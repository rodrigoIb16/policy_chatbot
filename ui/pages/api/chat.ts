import type { NextApiRequest, NextApiResponse } from 'next'
import { spawn } from 'child_process'
import path from 'path'

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  const { input } = req.body

  const scriptPath = path.resolve(process.cwd(), '../src/policy_agent.py')

  const pyProcess = spawn('python3', [scriptPath], {
    cwd: process.cwd().replace(/\/ui$/, ''),
    env: {
      ...process.env,
      CHAT_QUERY: input,
    },
  })

  let output = ''
  pyProcess.stdout.on('data', (data) => {
    output += data.toString()
  })

  pyProcess.stderr.on('data', (data) => {
    console.error('stderr:', data.toString())
  })

  pyProcess.on('close', () => {
    const lastLine = output.trim().split('\n').pop()
    res.status(200).json({ output: lastLine || "No response." })
  })
}
