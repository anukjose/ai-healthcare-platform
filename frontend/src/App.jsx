import { useState } from "react";

export default function App() {

  const [patientId, setPatientId] = useState("");
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loggedIn, setLoggedIn] = useState(false);


  // ---------------------------------------------------
  // KUBERNETES BACKEND API
  // ---------------------------------------------------
  // Backend exposed through Kubernetes NodePort Service
  //
  // phaseb-api-service
  // exposed externally via:
  //
  // http://localhost:30080
  // ---------------------------------------------------

  const API_URL = "http://localhost:30080/ask";


  // ---------------------------------------------------
  // PREVIOUS DOCKER COMPOSE CONFIG
  // ---------------------------------------------------
  /*
  Docker Compose backend exposure:

  const API_URL = "http://127.0.0.1:8002/ask";

  because backend container was exposed using:
  docker-compose port mapping.
  */


  // ---------------------------------------------------
  // PREVIOUS LOCAL FASTAPI CONFIG
  // ---------------------------------------------------
  /*
  Local laptop FastAPI backend:

  const API_URL = "http://127.0.0.1:8000/ask";
  */


  // ---------------------------------------------------
  // LOGIN
  // ---------------------------------------------------

  const handleLogin = () => {

    if (!patientId) return;

    setLoggedIn(true);
  };


  // ---------------------------------------------------
  // SEND QUESTION
  // ---------------------------------------------------

  const sendQuestion = async () => {

    if (!question) return;

    const userMessage = {
      role: "user",
      content: question
    };

    setMessages(prev => [...prev, userMessage]);

    try {

      const response = await fetch(
        API_URL,
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json"
          },

          body: JSON.stringify({
            patient_id: patientId,
            question: question
          })
        }
      );

      const data = await response.json();

      const aiMessage = {
        role: "assistant",

        content:
          typeof data.answer === "string"
            ? data.answer
            : JSON.stringify(data.answer, null, 2),

        queryType: data.query_type
      };

      setMessages(prev => [...prev, aiMessage]);

    } catch (error) {

      console.error(error);

      alert("API Error");
    }

    setQuestion("");
  };


  // ---------------------------------------------------
  // LOGIN SCREEN
  // ---------------------------------------------------

  if (!loggedIn) {

    return (

      <div className="min-h-screen bg-gradient-to-br from-slate-100 to-slate-200 flex items-center justify-center p-6">

        <div className="bg-white p-10 rounded-3xl shadow-2xl w-full max-w-md">

          <h1 className="text-3xl font-bold mb-2 text-center">
            Healthcare AI
          </h1>

          <p className="text-center text-slate-500 mb-8">
            Secure Patient Assistant
          </p>

          <input
            type="text"
            placeholder="Enter Patient ID"
            value={patientId}
            onChange={(e) => setPatientId(e.target.value)}
            className="w-full border border-slate-300 rounded-2xl px-5 py-4 mb-5 outline-none focus:ring-2 focus:ring-blue-400"
          />

          <button
            onClick={handleLogin}
            className="w-full bg-blue-600 hover:bg-blue-700 transition text-white py-4 rounded-2xl font-semibold shadow-lg"
          >
            Continue
          </button>

        </div>

      </div>
    );
  }


  // ---------------------------------------------------
  // CHAT SCREEN
  // ---------------------------------------------------

  return (

    <div className="min-h-screen bg-gradient-to-br from-slate-100 to-slate-200 flex items-center justify-center p-4">

      <div className="w-full max-w-5xl h-[92vh] bg-white rounded-3xl shadow-2xl flex flex-col overflow-hidden">

        {/* HEADER */}

        <div className="bg-blue-600 text-white px-6 py-5 flex justify-between items-center">

          <div>

            <h1 className="text-2xl font-bold">
              Healthcare AI Assistant
            </h1>

            <p className="text-sm opacity-80 mt-1">
              SQL • Vector • Hybrid Retrieval
            </p>

          </div>

          <div className="bg-white/20 px-4 py-2 rounded-2xl text-sm font-medium">
            Patient: {patientId}
          </div>

        </div>


        {/* CHAT WINDOW */}

        <div className="flex-1 overflow-y-auto p-6 bg-slate-50 space-y-6">

          {messages.length === 0 && (

            <div className="text-center text-slate-400 mt-20">

              <h2 className="text-2xl font-semibold mb-3">
                Ask healthcare questions
              </h2>

              <p>
                Example: What is latest CRP and summarize history?
              </p>

            </div>
          )}


          {messages.map((msg, index) => (

            <div
              key={index}
              className={
                msg.role === "user"
                  ? "flex justify-end"
                  : "flex justify-start"
              }
            >

              <div
                className={
                  msg.role === "user"
                    ? "bg-blue-600 text-white p-5 rounded-3xl rounded-br-md max-w-2xl shadow-lg"
                    : "bg-white border border-slate-200 p-5 rounded-3xl rounded-bl-md max-w-2xl shadow-md"
                }
              >

                {msg.role === "assistant" && (

                  <div className="text-xs text-blue-600 font-semibold mb-3 uppercase tracking-wide">
                    Engine: {msg.queryType}
                  </div>
                )}

                <pre className="whitespace-pre-wrap text-sm font-sans leading-7">
                  {msg.content}
                </pre>

              </div>

            </div>
          ))}

        </div>


        {/* INPUT */}

        <div className="border-t bg-white p-5 flex gap-3">

          <input
            type="text"
            placeholder="Ask healthcare question..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            className="flex-1 border border-slate-300 rounded-2xl px-5 py-4 outline-none focus:ring-2 focus:ring-blue-400"
          />

          <button
            onClick={sendQuestion}
            className="bg-blue-600 hover:bg-blue-700 transition text-white px-8 py-4 rounded-2xl font-semibold shadow-lg"
          >
            Send
          </button>

        </div>

      </div>

    </div>
  );
}