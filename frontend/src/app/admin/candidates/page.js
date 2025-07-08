'use client'

import Link from "next/link";
import downloadCandidateResume from "@/app/actions";
import Image from "next/image";
import {useState, useEffect} from 'react'


export default function Page() {
    const [candidates, setCandidates] = useState([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        const fetchCandidates = async () => {
            try {

                const data = await fetch('http://127.0.0.1:8000/admin/candidates/', {
                    method: 'GET',
                    headers: {
                        'X-ADMIN': '1'
                    },
                })
                const res = await data.json()
                setCandidates(res.results || [])
                console.log('fetch candidates:', candidates)
            } catch (error) {
                console.error('Failed to fetch candidates:', error)
            } finally {
                setLoading(false)
            }
        }
        fetchCandidates()
    }, [])
    if (loading) {
        return <div>Loading...</div>
    }
    return (
        <div
            className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
            <main className="flex flex-col gap-[32px] row-start-2 items-center sm:items-start">
                <h1 className="text-lg font-extrabold">HR System - Demo</h1>
                <h2 className="font-semibold">Admin interface</h2>
                <ul className="list-inside list-disc text-sm/6 text-center sm:text-left font-[family-name:var(--font-geist-mono)]">
                    <li className="mb-2">
                        Go back to, {" "}
                        <Link href="/" className="hover:bg-sky-200"><strong>main</strong></Link>
                    </li>
                </ul>
                <div className="flex gap-4 items-center flex-col sm:flex-row">
                    <div className="overflow-x-auto">
                        <table className="min-w-full bg-white border border-gray-300">
                            <thead className="bg-gray-50">
                            <tr>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-b">
                                    Candidate ID
                                </th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-b">
                                    Name
                                </th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-b">
                                    Date of Birth
                                </th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-b">
                                    Years of Experience
                                </th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-b">
                                    Department
                                </th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-b">
                                    Resume
                                </th>
                            </tr>
                            </thead>
                            <tbody className="bg-white divide-y divide-gray-200">
                            {!candidates || candidates.length === 0 ? (
                                <tr>
                                    <td colSpan="6" className="px-6 py-4 text-center text-gray-500">
                                        No candidates found
                                    </td>
                                </tr>
                            ) : (
                                candidates.map((candidate) => (
                                    <tr key={candidate.id} className="hover:bg-gray-50">
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                                            {candidate.id}
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                                            {candidate.full_name}
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                                            {candidate.date_of_birth}
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                                            {candidate.years_of_experience}
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                                            {candidate.department_id}
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                                                <span className="cursor-pointer hover:text-blue-600"
                                                      onClick={() => downloadCandidateResume(candidate.id)}> 📥 </span>
                                        </td>
                                    </tr>
                                ))
                            )}
                            </tbody>
                        </table>
                    </div>
                </div>
            </main>
            <footer className="row-start-3 flex gap-[24px] flex-wrap items-center justify-center">
                <span
                    className="flex items-center gap-2 hover:underline hover:underline-offset-4"
                >
                    <Image
                        aria-hidden
                        src="/window.svg"
                        alt="Window icon"
                        width={16}
                        height={16}
                    />
                    Demo HR System
                </span>
            </footer>
        </div>
    )
}
