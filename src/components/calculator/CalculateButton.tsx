interface CalculateButtonProps {
  onClick: () => void
}

export default function CalculateButton({ onClick }: CalculateButtonProps) {
  return (
    <button
      onClick={onClick}
      className="w-full py-3 px-4 bg-success-color hover:bg-success-light text-white font-semibold rounded-lg transition shadow-md"
    >
      חשב
    </button>
  )
}
