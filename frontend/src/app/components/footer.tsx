import {SvgLogo } from "@/components/icons";
import CircularGithubIcon from "@/components/icons/CircularGithubIcon";
import Link from "next/link";

export default function Footer() {
  const year = new Date().getFullYear();

  return (
    <footer className="w-full bg-viking-950 text-viking-100 px-6 py-12 md:px-12 lg:px-20 text-sm md:text-base">
      <div className="max-w-screen-xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-y-10 md:gap-12 lg:gap-16">
        <div className="flex flex-col items-center md:items-start text-center md:text-left -mt-5">
          <div className="flex items-center space-x-2">
            <SvgLogo className="w-48 h-24 text-viking-400" />
          </div>
          <p className="text-viking-300 leading-relaxed">
            Real-time patient progress tracking for surgical environments.
          </p>
          <div className="text-xs sm:text-sm text-viking-300 pt-4">
            &copy; {year} Live Orbit (SSB). All rights reserved.
          </div>
        </div>

        <div className="flex flex-col items-center md:items-start text-center md:text-left space-y-4">
          <h4 className="text-lg font-semibold text-viking-400">Quick Links</h4>
          <ul className="space-y-2">
            <li>
              <Link
                href="/"
                className="hover:text-viking-200 transition-colors"
              >
                Home
              </Link>
            </li>
            <li>
              <Link
                href="/Dashboard/statusboard"
                className="hover:text-viking-200 transition-colors"
              >
                Dashboard
              </Link>
            </li>
            <li>
              <Link
                href="/Auth"
                className="hover:text-viking-200 transition-colors"
              >
                Login
              </Link>
            </li>
          </ul>
        </div>

        <div className="flex flex-col items-center md:items-start text-center md:text-left space-y-4">
          <h4 className="text-lg font-semibold text-viking-400">
            Connect with Us
          </h4>
          <Link
            href="https://github.com/Ahmad-nba/SSB"
            className="flex items-center space-x-2 hover:text-viking-200 transition-colors cursor-pointer"
            target="_blank"
            rel="noopener noreferrer"
          >
            <CircularGithubIcon size={20} circleSize={32} />
            <span>View Project on GitHub</span>
          </Link>
        </div>
      </div>
    </footer>
  );
}
