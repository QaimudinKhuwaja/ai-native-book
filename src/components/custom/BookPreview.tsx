import React from 'react';

function BookPreview() {
  const chapters = [
    { id: 1, title: 'Introduction to AI-Native Development', description: 'Understand the core concepts.' },
    { id: 2, title: 'Foundations of AI-Native Systems', description: 'Explore key architectural patterns.' },
    { id: 3, title: 'Implementing AI-Native Workflows', description: 'Practical approaches and tools.' },
    { id: 4, title: 'Operationalizing AI-Native Solutions', description: 'Deployment and monitoring.' },
    { id: 5, title: 'The Future of AI-Native', description: 'Emerging trends and impact.' },
  ];

  return (
    <div className="container my-12">
      <h2 className="text-3xl font-bold text-center mb-8">Explore the Book</h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
        {chapters.map((chapter) => (
          <article
            key={chapter.id}
            className="bg-white dark:bg-gray-800 rounded-lg shadow-md hover:shadow-xl transform hover:-translate-y-1 transition duration-200 p-6 flex flex-col h-full"
            aria-labelledby={`chapter-${chapter.id}-title`}
          >
            <div className="flex items-start">
              <div className="flex-shrink-0 w-12 h-12 rounded-full bg-primary text-white flex items-center justify-center mr-4 font-bold">
                {chapter.id}
              </div>
              <h3 id={`chapter-${chapter.id}-title`} className="text-lg font-semibold">{chapter.title}</h3>
            </div>

            <p className="text-gray-600 dark:text-gray-300 mt-4 flex-grow">{chapter.description}</p>

            <div className="mt-6">
              <a
                href={`/docs/${chapter.id}-chapter-slug`}
                className="button button--primary"
                aria-label={`Read Chapter ${chapter.id}: ${chapter.title}`}
              >
                Read Chapter {chapter.id}
              </a>
            </div>
          </article>
        ))}
      </div>
    </div>
  );
}

export default BookPreview;
