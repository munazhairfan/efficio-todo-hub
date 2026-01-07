export function SectionDivider({
  fromColor,
  toColor,
  className = "",
}: {
  fromColor: string
  toColor: string
  className?: string
}) {
  return (
    <div
      className={`relative w-full h-16 md:h-24 overflow-hidden -mt-px ${className}`}
      style={{ backgroundColor: fromColor }}
    >
      <svg
        className="absolute top-0 left-0 w-full h-full"
        viewBox="0 0 1440 320"
        preserveAspectRatio="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          fill={toColor}
          d="M0,160L48,176C96,192,192,224,288,224C384,224,480,192,576,165.3C672,139,768,117,864,128C960,139,1056,181,1152,197.3C1248,213,1344,203,1392,197.3L1440,192L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"
        ></path>
        <path
          fill="none"
          stroke="black"
          strokeWidth="0"
          d="M0,160L48,176C96,192,192,224,288,224C384,224,480,192,576,165.3C672,139,768,117,864,128C960,139,1056,181,1152,197.3C1248,213,1344,203,1392,197.3L1440,192"
        ></path>
      </svg>
    </div>
  )
}
