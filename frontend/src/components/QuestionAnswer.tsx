"use client";

import { type FormEvent, useState } from "react";

type SourceInfo = {
  filename: string;
  chunk_index: number;
  similarity_score: number;
  text_preview: string;
};

type QuestionAnswerResponse = {
  question: string;
  answer: string;
  source_count: number;
  sources: SourceInfo[];
};

const QA_URL = "http://127.0.0.1:8000/qa/ask";
const TOP_K = 3;

export default function QuestionAnswer() {
  const [question, setQuestion] = useState("");
  const [answerResult, setAnswerResult] =
    useState<QuestionAnswerResponse | null>(null);
  const [errorMessage, setErrorMessage] = useState("");
  const [isAsking, setIsAsking] = useState(false);

  async function handleAskQuestion(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const trimmedQuestion = question.trim();

    if (!trimmedQuestion) {
      setErrorMessage("Please enter a question before asking.");
      return;
    }

    setIsAsking(true);
    setErrorMessage("");
    setAnswerResult(null);

    try {
      const response = await fetch(QA_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: trimmedQuestion,
          top_k: TOP_K,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Question request failed.");
      }

      setAnswerResult(data as QuestionAnswerResponse);
    } catch (error) {
      const message =
        error instanceof Error ? error.message : "Question request failed.";

      setErrorMessage(message);
    } finally {
      setIsAsking(false);
    }
  }

  return (
    <section
      aria-label="Question answering"
      className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm"
    >
      <div>
        <p className="text-sm font-semibold text-slate-950">Ask a question</p>
        <p className="mt-1 text-sm leading-6 text-slate-500">
          Upload a file first. Stored context resets when the backend restarts.
        </p>
      </div>

      <form onSubmit={handleAskQuestion} className="mt-5 space-y-4">
        <label className="block">
          <span className="text-sm font-medium text-slate-700">Question</span>
          <textarea
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            disabled={isAsking}
            rows={4}
            placeholder="What is this file about?"
            className="mt-2 block w-full resize-none rounded-xl border border-slate-300 bg-white px-3 py-3 text-sm leading-6 text-slate-900 shadow-sm outline-none placeholder:text-slate-400 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100 disabled:cursor-not-allowed disabled:bg-slate-50 disabled:text-slate-500"
          />
        </label>

        <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <p className="text-xs text-slate-500">
            Uses top_k={TOP_K} relevant chunks from the in-memory vector store.
          </p>
          <button
            type="submit"
            disabled={!question.trim() || isAsking}
            className="rounded-lg bg-indigo-600 px-5 py-3 text-sm font-semibold text-white shadow-sm hover:bg-indigo-700 disabled:cursor-not-allowed disabled:bg-slate-300"
          >
            {isAsking ? "Searching relevant chunks..." : "Ask question"}
          </button>
        </div>
      </form>

      {errorMessage && (
        <div className="mt-4 rounded-lg border border-rose-200 bg-rose-50 p-3 text-sm text-rose-700">
          {errorMessage}
        </div>
      )}

      {answerResult && (
        <div className="mt-5 space-y-4">
          <div className="rounded-xl border border-indigo-100 bg-indigo-50 p-4">
            <p className="text-xs font-medium uppercase tracking-wide text-indigo-700">
              Answer
            </p>
            <p className="mt-2 text-sm leading-6 text-slate-800">
              {answerResult.answer}
            </p>
          </div>

          <div>
            <div className="flex items-center justify-between gap-4">
              <p className="text-sm font-semibold text-slate-950">Sources</p>
              <p className="text-sm text-slate-500">
                {answerResult.source_count} found
              </p>
            </div>

            {answerResult.sources.length > 0 ? (
              <div className="mt-3 grid gap-3">
                {answerResult.sources.map((source) => (
                  <article
                    key={`${source.filename}-${source.chunk_index}`}
                    className="rounded-xl border border-slate-200 bg-slate-50 p-4"
                  >
                    <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
                      <p className="font-mono text-xs font-medium text-indigo-700">
                        {source.filename} - chunk {source.chunk_index}
                      </p>
                      <p className="text-xs text-slate-500">
                        similarity {source.similarity_score}
                      </p>
                    </div>
                    <p className="mt-3 text-sm leading-6 text-slate-600">
                      {source.text_preview}
                    </p>
                  </article>
                ))}
              </div>
            ) : (
              <div className="mt-3 rounded-xl border border-amber-200 bg-amber-50 p-4 text-sm leading-6 text-amber-800">
                No sources were returned. Upload a file first, then ask your
                question again.
              </div>
            )}
          </div>
        </div>
      )}
    </section>
  );
}
