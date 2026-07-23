import BackendStatus from "@/src/components/BackendStatus";
import FileUploader from "@/src/components/FileUploader";
import QuestionAnswer from "@/src/components/QuestionAnswer";

const features = [
  {
    title: "Upload supported files",
    description:
      "Add code, notes, markdown, CSV, and text files to prepare them for search.",
  },
  {
    title: "Extract and chunk text",
    description:
      "Read file content, split it into useful chunks, and keep the structure simple.",
  },
  {
    title: "Local semantic search",
    description:
      "Use local embeddings to retrieve the most relevant context from uploaded files.",
  },
  {
    title: "Ask questions with sources",
    description:
      "Ask against retrieved context and show source previews from matching chunks.",
  },
];

const pipelineSteps = ["Upload", "Extract", "Chunk", "Embed", "Search", "Answer"];

const statusItems = [
  "FastAPI backend running",
  "File upload working",
  "Local embeddings working",
  "Vector search working",
  "Question answering API working",
  "Frontend interface in progress",
];

export default function Home() {
  return (
    <main className="min-h-screen bg-slate-50 text-slate-950">
      <header className="sticky top-0 z-20 border-b border-slate-200 bg-white/85 backdrop-blur">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-5 py-4 sm:px-6">
          <a href="#" className="text-base font-semibold tracking-tight">
            DevDesk Agent
          </a>

          <div className="flex items-center gap-3">
            <nav
              aria-label="Main navigation"
              className="hidden items-center gap-6 text-sm font-medium text-slate-600 md:flex"
            >
              <a href="#features" className="hover:text-slate-950">
                Features
              </a>
              <a href="#pipeline" className="hover:text-slate-950">
                Pipeline
              </a>
              <a href="#status" className="hover:text-slate-950">
                Status
              </a>
            </nav>

            <a
              href="#pipeline"
              className="rounded-lg border border-slate-300 bg-white px-3.5 py-2 text-sm font-medium text-slate-800 shadow-sm hover:border-slate-400"
            >
              Open Docs
            </a>
          </div>
        </div>
      </header>

      <section className="px-5 py-16 sm:px-6 sm:py-20">
        <div className="mx-auto grid max-w-6xl gap-10 lg:grid-cols-[1fr_0.85fr] lg:items-center">
          <div>
            <p className="inline-flex rounded-full border border-indigo-200 bg-indigo-50 px-3 py-1 text-sm font-medium text-indigo-700">
              Local RAG workspace
            </p>

            <h1 className="mt-6 max-w-3xl text-4xl font-semibold tracking-tight text-slate-950 sm:text-5xl">
              Understand your project files with local AI search.
            </h1>

            <p className="mt-5 max-w-2xl text-base leading-7 text-slate-600 sm:text-lg">
              Upload code, notes, and documents. DevDesk Agent extracts text,
              creates chunks, generates local embeddings, and helps you ask
              questions with source previews.
            </p>

            <div className="mt-8 flex flex-col gap-3 sm:flex-row">
              <a
                href="#features"
                className="rounded-lg bg-indigo-600 px-5 py-3 text-center text-sm font-semibold text-white shadow-sm hover:bg-indigo-700"
              >
                Explore Features
              </a>
              <a
                href="#pipeline"
                className="rounded-lg border border-slate-300 bg-white px-5 py-3 text-center text-sm font-semibold text-slate-800 shadow-sm hover:border-slate-400"
              >
                View Pipeline
              </a>
            </div>
          </div>

          <aside
            aria-label="Product preview"
            className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm"
          >
            <div className="flex items-center justify-between border-b border-slate-200 pb-4">
              <div>
                <p className="text-sm font-semibold text-slate-950">
                  Workspace preview
                </p>
                <p className="mt-1 text-sm text-slate-500">
                  Local document context
                </p>
              </div>
              <span className="rounded-full bg-indigo-50 px-3 py-1 text-xs font-medium text-indigo-700">
                MVP
              </span>
            </div>

            <div className="divide-y divide-slate-100">
              <div className="py-4">
                <div className="flex items-center justify-between gap-4 text-sm">
                  <span className="font-medium text-slate-700">Upload status</span>
                  <span className="text-slate-500">Ready for files</span>
                </div>
              </div>

              <div className="py-4">
                <div className="flex items-center justify-between gap-4 text-sm">
                  <span className="font-medium text-slate-700">Stored chunks</span>
                  <span className="text-slate-500">From uploaded content</span>
                </div>
              </div>

              <div className="py-4">
                <p className="text-sm font-medium text-slate-700">Search query</p>
                <p className="mt-2 rounded-lg border border-slate-200 bg-slate-50 px-3 py-2 font-mono text-sm text-slate-600">
                  Where is the upload logic?
                </p>
              </div>

              <div className="py-4">
                <p className="text-sm font-medium text-slate-700">
                  Source preview
                </p>
                <div className="mt-2 rounded-lg border border-slate-200 bg-slate-50 p-3">
                  <p className="font-mono text-xs text-indigo-700">
                    routes/upload.py - chunk 0
                  </p>
                  <p className="mt-2 text-sm leading-6 text-slate-600">
                    File text is extracted, chunked, embedded, and stored for
                    local retrieval.
                  </p>
                </div>
              </div>
            </div>
          </aside>
        </div>
      </section>

      <section className="px-5 pb-8 sm:px-6">
        <div className="mx-auto max-w-6xl space-y-4">
          <div className="grid gap-4 lg:grid-cols-[0.85fr_1.15fr]">
            <BackendStatus />
            <FileUploader />
          </div>
          <QuestionAnswer />
        </div>
      </section>

      <section id="features" className="px-5 py-14 sm:px-6">
        <div className="mx-auto max-w-6xl">
          <div className="max-w-2xl">
            <h2 className="text-2xl font-semibold tracking-tight text-slate-950 sm:text-3xl">
              Focused features for the MVP
            </h2>
            <p className="mt-3 text-base leading-7 text-slate-600">
              The product stays intentionally practical: upload, process,
              retrieve, and answer from local project context.
            </p>
          </div>

          <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {features.map((feature) => (
              <article
                key={feature.title}
                className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm"
              >
                <div className="mb-5 h-1.5 w-10 rounded-full bg-indigo-600" />
                <h3 className="text-base font-semibold text-slate-950">
                  {feature.title}
                </h3>
                <p className="mt-3 text-sm leading-6 text-slate-600">
                  {feature.description}
                </p>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section
        id="pipeline"
        className="border-y border-slate-200 bg-white px-5 py-14 sm:px-6"
      >
        <div className="mx-auto max-w-6xl">
          <div className="max-w-2xl">
            <h2 className="text-2xl font-semibold tracking-tight text-slate-950 sm:text-3xl">
              Simple local RAG pipeline
            </h2>
            <p className="mt-3 text-base leading-7 text-slate-600">
              A small set of backend steps turns uploaded files into searchable
              context for question answering.
            </p>
          </div>

          <div className="mt-8 grid gap-3 sm:grid-cols-2 lg:grid-cols-6">
            {pipelineSteps.map((step, index) => (
              <div
                key={step}
                className="rounded-xl border border-slate-200 bg-slate-50 p-4"
              >
                <p className="font-mono text-xs font-medium text-slate-400">
                  0{index + 1}
                </p>
                <p className="mt-3 text-sm font-semibold text-slate-900">
                  {step}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section id="status" className="px-5 py-14 sm:px-6">
        <div className="mx-auto max-w-6xl">
          <div className="max-w-2xl">
            <h2 className="text-2xl font-semibold tracking-tight text-slate-950 sm:text-3xl">
              Current build status
            </h2>
            <p className="mt-3 text-base leading-7 text-slate-600">
              The backend foundation is working, and the frontend is being
              shaped into a usable product interface.
            </p>
          </div>

          <div className="mt-8 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {statusItems.map((item) => (
              <div
                key={item}
                className="flex items-center gap-3 rounded-xl border border-slate-200 bg-white p-4 shadow-sm"
              >
                <span
                  aria-hidden="true"
                  className="h-2.5 w-2.5 rounded-full bg-indigo-600"
                />
                <p className="text-sm font-medium text-slate-700">{item}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <footer className="border-t border-slate-200 bg-white px-5 py-8 sm:px-6">
        <div className="mx-auto max-w-6xl">
          <p className="text-sm text-slate-500">
            Built as a practical AI engineering project.
          </p>
        </div>
      </footer>
    </main>
  );
}
