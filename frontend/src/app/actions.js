'use client'

export default async function downloadCandidateResume(candidate_id) {
  try {
    console.log('Download called')
    const response = await fetch(`http://127.0.0.1:8000/admin/candidates/${candidate_id}/resume-download/`, {
      method: 'GET',
      headers: {
        'X-ADMIN': '1'
      },
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const blob = await response.blob()

    // Get filename from Content-Disposition header or use default
    const contentDisposition = response.headers.get('Content-Disposition')
    let filename = `candidate_${candidate_id}_resume.pdf`

    if (contentDisposition) {
      const matches = contentDisposition.match(/filename="(.+)"/)
      if (matches) {
        filename = matches[1]
      }
    }

    // Create and trigger download
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = filename
    link.style.display = 'none'

    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)

    // Clean up
    URL.revokeObjectURL(url)

  } catch (error) {
    console.error('Download failed:', error)
  }
}

