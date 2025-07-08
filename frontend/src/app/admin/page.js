import Link from "next/link";
import {saveAdminName} from '@/app/actions'
import Image from "next/image";


export default function Page() {

  return (
      <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <main className="flex flex-col gap-[32px] row-start-2 items-center sm:items-start">
        <h1 className="text-lg font-extrabold">HR System - Demo</h1>
        <h2 className="font-semibold">Admin interface</h2>
        <ol className="list-inside list-decimal text-sm/6 text-center sm:text-left font-[family-name:var(--font-geist-mono)]">
          <li className="mb-2 tracking-[-.01em]">
            [admin], {" "}
            <Link href="/admin/candidates/" className="hover:bg-sky-200"><strong>List candidates & download resumes!</strong></Link>
          </li>
          <li className="mb-2 tracking-[-.01em]">
            Go back to, {" "}
            <Link href="/" className="hover:bg-sky-200"><strong>main</strong></Link>
          </li>
        </ol>
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
  );
}