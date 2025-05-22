import React, { useEffect, useState } from "react";
import Layout from "./Layout";

interface UserAnswersProps {
  email: string;
  onBack: () => void;
}

interface Answer {
  date: string;
  answers: {
    question: string;
    answer: string;
  }[];
}

const UserAnswers: React.FC<UserAnswersProps> = ({ email, onBack }) => {
  const [answers, setAnswers] = useState<Answer[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // TODO: Implement fetchUserAnswers API call
    // For now, using mock data
    setAnswers([
      {
        date: "2024-03-20",
        answers: [
          {
            question: "What did you accomplish today?",
            answer: "Completed the frontend redesign and implemented new features.",
          },
          {
            question: "What are your priorities for tomorrow?",
            answer: "Testing the new features and fixing any bugs.",
          },
        ],
      },
    ]);
    setLoading(false);
  }, [email]);

  return (
    <Layout>
      <div className="space-y-6">
        <div className="flex items-center space-x-4">
          <button
            onClick={onBack}
            className="text-gray-600 hover:text-gray-900 flex items-center space-x-2"
          >
            <svg
              className="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M10 19l-7-7m0 0l7-7m-7 7h18"
              />
            </svg>
            <span>Back to Team</span>
          </button>
          <h2 className="text-2xl font-bold text-gray-900">
            {email}'s Check-in History
          </h2>
        </div>

        {loading ? (
          <div className="flex justify-center items-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          </div>
        ) : (
          <div className="space-y-6">
            {answers.map((day, index) => (
              <div
                key={day.date}
                className="bg-white rounded-lg shadow p-6 space-y-4"
              >
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-semibold text-gray-900">
                    {new Date(day.date).toLocaleDateString("en-US", {
                      weekday: "long",
                      year: "numeric",
                      month: "long",
                      day: "numeric",
                    })}
                  </h3>
                </div>
                <div className="space-y-4">
                  {day.answers.map((qa, qaIndex) => (
                    <div key={qaIndex} className="space-y-2">
                      <h4 className="font-medium text-gray-700">{qa.question}</h4>
                      <p className="text-gray-600 whitespace-pre-wrap">{qa.answer}</p>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </Layout>
  );
};

export default UserAnswers;