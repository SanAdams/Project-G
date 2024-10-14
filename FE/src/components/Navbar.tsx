import { useState } from "react"

const Navbar = () => {

    return (
        <nav className="bg-white">
            <div className="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4">
                <div className="flex flex-row items-center justify-center h-8">

                    <a href="" className="flex items-center space-x-3 rtl:space-x-reverse mb-4">
                        {/* <img src=".././public/projglogo1.webp" className="h-20" alt="Project G" />
                    <img src=".././public/projgsvg.svg" className="h-20" alt="Project G" /> */}
                        <img src=".././public/projgsvgg.svg" className="h-16 mt-6" alt="Project G" />
                        <span className="self-center text-2xl font-semibold whitespace-nowrap">Project G!</span>
                    </a>
                </div>
                <button data-collapse-toggle="navbar-default" type="button" className="inline-flex items-center w-10 h-10 justify-center text-sm text-gray-500 rounded-lg md:hidden hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200" aria-controls="navbar-default" aria-expanded="false">
                    <span className="sr-only">Open main menu</span>
                    <svg className="w-5 h-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 17 14">
                        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1 1h15M1 7h15M1 13h15" />
                    </svg>
                </button>
                <div className="hidden md:block md:w-auto" id="navbar-default">
                    <ul className="font-medium flex flex-col p-4 md:p-0 mt-4 border border-gray-100 rounded-lg bg-gray-50 md:flex-row md:space-x-8 rtl:space-x-reverse md:mt-0 md:border-0 md:bg-white">
                        <li>
                            <button className="block py-2 px-3 text-goonblack border-2 border-goonpurple rounded" aria-current="page">Sign In</button>
                        </li>

                    </ul>
                </div>
            </div>
            <div className="flex flex-row items-center justify-around  text-goonwhite border-2 border-goonpurple mx-10 rounded-lg p-2">
                <button className="font-bold rounded-lg p-2 bg-goonpurple min-w-20 max-w-fit">
                    <a href="#">Map</a>
                </button>
                <button className="font-bold rounded-lg p-2 bg-goonpurple min-w-20 max-w-fit">
                    <a href="#">Playground</a>
                </button>
                <button className="font-bold rounded-lg p-2 bg-goonpurple min-w-20 max-w-fit">
                    <a href="#">Insights</a>
                </button>
            </div>
        </nav>
    )
}

export default Navbar
