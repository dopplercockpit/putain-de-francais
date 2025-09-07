// frontend/app/layout.tsx

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-black text-white">
        <main className="max-w-2xl mx-auto p-6">{children}</main>
      </body>
    </html>
  );
}


