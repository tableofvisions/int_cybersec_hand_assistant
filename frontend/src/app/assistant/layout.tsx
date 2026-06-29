import Footer from "@/components/assistant/shared/Footer";
import Navbar from "@/components/assistant/shared/Navbar";
import BetaBanner from "@/components/shared/BetaBanner";
import SessionGuard from "@/components/assistant/shared/SessionGuard";
import Providers from "../providers";

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <Providers>
        <BetaBanner />
        <div className="flex min-h-screen flex-col lg:flex-row flex-wrap bg-contrast-verylight overflow-x-hidden">
          <SessionGuard />
          <Navbar />
          <main className="grow flex-1 flex flex-row justify-center my-5 px-5 w-full">
            <div className="w-full max-w-[1200px]">{children}</div>
          </main>
          <Footer />
        </div>
      </Providers>
    </>
  );
}
