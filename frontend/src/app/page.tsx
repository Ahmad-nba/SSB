"use client";
import { cardData } from "@/utils/cardData";
import AuthModule from "./Auth/page";
import HomeCard from "./components/homeCard";
import Image from "next/image";
import logo from "../../public/assets/logo.svg";
import { useAuth } from "@/Features/auth/hooks/useAuth";
import { FiUser } from "react-icons/fi";
import { useAuthStore } from "@/Features/auth/store/useAuthStore";

export default function HomePage() {
  const { isLoggedIn, fullName, role } = useAuth();
  const logout = useAuthStore((state) => state.logout);
  return (
    <main>
      {/* intro capture head */}
      <section className="flex flex-col justify-center items-center mt-6">
        <div className="flex flex-col sm:w-[40%] w-[80%] justify-center items-center">
          <Image
            src={logo}
            alt="App Logo"
            width={180}
            height={90}
            className="object-contain p-1"
          />
          {/* <h1 className="text-2xl font-black font-sans">Live Orbit</h1> */}
          <h3 className="text-gray-600 text-center">
            Keeping families, loved ones informed and surgical teams coordinated
            with real time patient progress tracking{" "}
          </h3>
        </div>
      </section>
      {/* card section  */}
      <section className="grid mt-4  gap-y-4 sm:gap-x-4 gap-x-2 grid-cols-2 sm:grid-cols-4">
        {cardData.map((card) => {
          return (
            <HomeCard
              key={card.desc}
              Icon={card.Icon}
              header={card.header}
              desc={card.desc}
            />
          );
        })}
      </section>
      {/* auth module */}
      <section className="mx-auto mt-10">
        {!isLoggedIn ? (
          <AuthModule />
        ) : (
          <section className="flex flex-col mx-auto mb-4 py-2 justify-center items-center shadow w-[80%] sm:w-[40%] space-y-2">
            <section className="flex justify-center items-center space-x-2">
              <FiUser className="size-9" />({role})
            </section>
            <p>Logged in as</p>
            <p>{fullName} </p>
            <button
              onClick={() => logout()}
              className="bg-red-400 p-2 w-[80%] mx-[10%] text-white rounded"
            >
              Log Out
            </button>
          </section>
        )}
      </section>
    </main>
  );
}
// land page
