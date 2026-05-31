import { ShieldCheck } from "lucide-react";
import { useState } from "react";
import axios from "axios";

function App() {
  const [news, setNews] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const analyzeNews = async () => {
    if (!news.trim()) {
      alert("Please enter news text");
      return;
    }

    setLoading(true);

    try {
      const response = await axios.post(
        "https://fakeshield-ai-59th.onrender.com/predict",
        {
          news: news,
        }
      );

      setResult(response.data);
    } catch (error) {
      console.error(error);
      alert("Unable to connect to Flask API");
    }

    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-blue-950 text-white">

      {/* Navbar */}
      <nav className="flex justify-between items-center px-8 py-6">
        <div className="flex items-center gap-3">
          <ShieldCheck size={35} />
          <h1 className="text-3xl font-bold">
            FakeShield AI
          </h1>
        </div>

        <button className="px-5 py-2 rounded-xl bg-white/10 backdrop-blur-md border border-white/20 hover:bg-white/20 transition">
          Cloud Project
        </button>
      </nav>

      {/* Hero */}
      <div className="flex justify-center px-6 mt-10">
        <div className="bg-white/10 backdrop-blur-xl border border-white/20 rounded-3xl p-10 max-w-6xl w-full shadow-2xl">

          <h1 className="text-6xl font-extrabold text-center mb-5">
            Detect Fake News with AI
          </h1>

          <p className="text-center text-slate-300 text-xl mb-8">
            Cloud-Powered Fake News Detection using Machine Learning,
            NLP, Flask API and React.
          </p>

          {/* Input Box */}
          <textarea
            value={news}
            onChange={(e) => setNews(e.target.value)}
            placeholder="Paste your news article here..."
            className="w-full h-64 rounded-2xl bg-black/20 border border-white/20 p-5 text-lg outline-none resize-none"
          />

          {/* Button */}
          <div className="flex justify-center mt-8">
            <button
              onClick={analyzeNews}
              className="px-10 py-4 rounded-2xl bg-blue-600 hover:bg-blue-700 transition text-lg font-semibold"
            >
              {loading ? "Analyzing..." : "Analyze News"}
            </button>
          </div>

          {/* Result */}
          {result && (
            <div className="mt-10">

              <div
                className={`rounded-2xl p-8 text-center border ${
                  result.prediction === "Fake News"
                    ? "bg-red-500/20 border-red-500"
                    : "bg-green-500/20 border-green-500"
                }`}
              >
                <h2 className="text-4xl font-bold mb-4">
                  {result.prediction === "Fake News"
                    ? "❌ Fake News"
                    : "✅ Real News"}
                </h2>

                <p className="text-2xl mb-5">
                  Confidence: {result.confidence}%
                </p>

                {/* Progress Bar */}
                <div className="w-full bg-gray-700 rounded-full h-5">
                  <div
                    className={`h-5 rounded-full ${
                      result.prediction === "Fake News"
                        ? "bg-red-500"
                        : "bg-green-500"
                    }`}
                    style={{
                      width: `${result.confidence}%`,
                    }}
                  ></div>
                </div>
              </div>

            </div>
          )}
        </div>
      </div>

      {/* Features Section */}
      <div className="grid md:grid-cols-3 gap-6 px-8 py-16 max-w-7xl mx-auto">

        <div className="bg-white/10 border border-white/10 rounded-3xl p-6 backdrop-blur-lg">
          <h3 className="text-2xl font-bold mb-3">
            NLP Processing
          </h3>
          <p className="text-slate-300">
            Cleans and preprocesses news text using stopword removal,
            tokenization and stemming.
          </p>
        </div>

        <div className="bg-white/10 border border-white/10 rounded-3xl p-6 backdrop-blur-lg">
          <h3 className="text-2xl font-bold mb-3">
            Machine Learning
          </h3>
          <p className="text-slate-300">
            Uses TF-IDF Vectorization and Logistic Regression
            for classification.
          </p>
        </div>

        <div className="bg-white/10 border border-white/10 rounded-3xl p-6 backdrop-blur-lg">
          <h3 className="text-2xl font-bold mb-3">
            Cloud Deployment
          </h3>
          <p className="text-slate-300">
            Deployable using Vercel, Render and MongoDB Atlas.
          </p>
        </div>

      </div>

    </div>
  );
}

export default App;