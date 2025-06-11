import type { NextApiRequest, NextApiResponse } from 'next'

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const { input } = req.body

  try {
    const response = await fetch('https://policy-chatbot-lt2w-git-main-rodrigoib16s-projects.vercel.app/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ input }),
    })

    if (!response.ok) {
      throw new Error(`Backend error: ${response.statusText}`)
    }

    const data = await response.json()
    res.status(200).json({ output: data.output || "No response." })
  } catch (err) {
    console.error('Error calling backend:', err)
    res.status(500).json({ output: "Sorry, something went wrong." })
  }
}
