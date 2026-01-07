import { Card } from "@/components/ui/card"

interface FeatureCardProps {
  title: string
  description: string
  icon: string
}

export function FeatureCard({ title, description, icon }: FeatureCardProps) {
  return (
    <Card className="h-40 flex flex-col py-3 justify-evenly border-4 border-code-gray bg-confetti shadow-[8px_8px_0px_0px_rgba(45,45,45,1)] hover:-translate-y-2 transition-transform duration-300">
      {/* <div className="w-20 h-20 mb-6 mx-auto bg-mint-julep rounded-2xl border-4 border-code-gray flex items-center justify-center overflow-hidden">
        <img
          src={`/.jpg?key=63c2b&height=80&width=80&query=${encodeURIComponent(icon)}`}
          alt={title}
          className="w-16 h-16"
        />
      </div> */}
      <h3 className="text-2xl font-black text-code-gray text-center">{title}</h3>
      <p className="text-code-gray/80 text-center font-medium leading-relaxed">{description}</p>
    </Card>
  )
}
