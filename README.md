# EPUB Translator

Transform your digital books into any language you want to read, making world literature accessible to everyone. This OOMOL block provides a visual, no-code interface to translate EPUB books while preserving their structure and formatting.

<div align="center">

![Translation Effect](https://raw.githubusercontent.com/oomol-lab/epub-translator/main/docs/images/translation.png)

[![Watch the Tutorial](https://raw.githubusercontent.com/oomol-lab/epub-translator/main/docs/images/link2youtube.png)](https://www.youtube.com/watch?v=QsAdiskxfXI)

</div>

## What This Does

Have you ever found an amazing book that's only available in a language you don't speak fluently? This block solves that problem. It takes your digital books (in EPUB format) and translates them into your preferred language through an intuitive visual workflow, making reading accessible and enjoyable in the language you're most comfortable with.

Whether it's a bestseller from another country, academic material, or a classic work of literature, you can now read it in your language without waiting for official translations.

## Why Use This Block

- **Visual workflow interface** - No coding required, simply drag and connect blocks to create your translation pipeline
- **Read books in your native language** - No more struggling with foreign language books or missing out on great content
- **Keep the original alongside the translation** - See both languages side-by-side, perfect for language learners who want to improve while reading
- **Preserve the book's look and feel** - The translated book maintains the same formatting, structure, and reading experience as the original
- **Support for many languages** - Translate to and from English, Chinese, Spanish, French, German, Japanese, Korean, Portuguese, Russian, Italian, Arabic, and Hindi
- **Fast and reliable** - Intelligent translation that handles complex book structures and maintains consistency throughout
- **Real-time progress monitoring** - Watch your translation progress visually in the OOMOL interface

## Getting Started with OOMOL

### Installation

1. Open OOMOL Studio
2. Search for `books-translator` in the package marketplace
3. Click "Install" to add the block to your workspace
4. The block will appear in your block panel, ready to use

### Basic Usage

1. **Add the Block** - Drag the "Books Translator" block onto your canvas
2. **Configure Inputs**:
   - **Source EPUB**: Click the file picker to select your EPUB book
   - **Target Language**: Choose from 12 supported languages (default: Chinese)
   - **Submit Mode**: Select "Append" for bilingual output or "Replace" for translation only
3. **Run the Flow** - Click the run button and watch the progress
4. **Get Your Book** - The translated EPUB will be saved to your specified location

## Features

### Two Translation Modes

Choose how you want your translated book to look:

- **Append Mode (Recommended)** - Creates a bilingual book where each paragraph is followed by its translation. Perfect for language learners who want to compare the original with the translation, or anyone who wants to understand nuances in the text.

- **Replace Mode** - Creates a clean translated version with only the target language. Ideal when you simply want to read the book in your language without the original text.

### Supported Languages

The block supports translation between these languages:
- English
- Chinese (Simplified)
- Spanish
- French
- German
- Japanese
- Korean
- Portuguese
- Russian
- Italian
- Arabic
- Hindi

### Advanced Options

For power users who want more control, the block provides advanced settings:

- **Concurrency (1-8)** - Control how many sections are translated simultaneously. Higher values speed up translation but use more resources. Default: 4

- **Max Group Tokens (≥350)** - Control the size of text chunks sent for translation. Larger values may improve context understanding but take longer per chunk. Default: 2600

- **Custom Prompt** - Add specific instructions to guide the translation style:
  - "Keep character names in their original form"
  - "Use formal language tone"
  - "Preserve cultural references"
  - "Maintain technical terminology"
  - "Adjust for children's reading level"

- **Translated Path** - Choose where to save your translated book. If not specified, it will be saved in the session directory

- **LLM Configuration** - Fine-tune the translation model settings:
  - Model selection (default: deepseek-chat)
  - Temperature (0-1): Controls creativity vs consistency
  - Top P (0-1): Controls response diversity
  - Max Tokens: Maximum length of translation output

## Building Translation Workflows

Since this is an OOMOL block, you can combine it with other blocks to create powerful workflows:

### Simple Translation

```
[File Input] → [Books Translator] → [File Output]
```

### Batch Translation

```
[File List] → [For Each Loop] → [Books Translator] → [Collect Results]
```

### Translation with Notification

```
[File Input] → [Books Translator] → [Send Email Notification]
                                   → [Upload to Cloud Storage]
```

### Pre-processing Pipeline

```
[EPUB Input] → [Validate Format] → [Books Translator] → [Quality Check] → [Output]
```

## Tips for Best Results

- **Book quality matters** - Books with clean, well-formatted text translate better than those with formatting issues
- **Be patient with long books** - Novels and longer works take more time, but the quality is worth the wait. A typical novel takes 5-15 minutes depending on length
- **Try custom instructions** - If the first translation isn't quite what you want, add specific guidance in the Custom Prompt field and try again
- **Use bilingual mode for learning** - Even if you're fluent in the target language, seeing both versions helps you appreciate translation choices
- **Monitor progress** - The OOMOL interface shows real-time progress, so you can see exactly which sections are being translated

## What Makes It Special

Unlike simple word-by-word translators, this tool understands context and maintains the natural flow of the story or content. It preserves chapter breaks, formatting, and even the author's writing style as much as possible in the target language.

The translation process is smart enough to:

- Maintain consistency with character names and terms throughout the entire book
- Respect the original paragraph and sentence structure for better readability
- Keep special formatting like emphasis, quotes, lists, and chapter headings
- Preserve the reading order and chapter organization exactly as the author intended
- Handle complex book structures including footnotes, tables of contents, and multi-part stories
- Adapt to different book genres, from fiction to technical manuals

The block uses advanced language understanding to ensure translations feel natural and readable, not mechanical or awkward like basic translation tools.

## Technical Details

This block is a visual wrapper around the [epub-translator](https://github.com/oomol-lab/epub-translator) library, designed specifically for the OOMOL visual programming environment. It provides:

- Automatic progress reporting through the OOMOL context
- Visual preview of translation progress
- Seamless integration with other OOMOL blocks
- File path handling compatible with OOMOL's session management

## Who This Is For

- **Avid readers** who want to enjoy books not available in their language
- **Students** learning a new language who want reading practice with support
- **Parents** who want to read books to their children in a specific language
- **Travelers** who collect books from different countries and want to understand them
- **Researchers** who need to access academic content across language barriers
- **Book clubs** that want to read international bestsellers before official translations
- **Visual programmers** who prefer no-code solutions over writing Python scripts
- **Anyone** curious about literature from other cultures

## Requirements

- An OOMOL Studio installation
- An EPUB book file you want to translate
- A few minutes to let the translation complete (time varies based on book length)
- An e-reader or reading app to enjoy your translated book (like Apple Books, Google Play Books, Calibre, or any EPUB-compatible app)

## Support

- For block-specific issues, please report at: https://github.com/oomol-flows/books-translator-ng/issues
- For the underlying translation library: https://github.com/oomol-lab/epub-translator/issues
- For OOMOL Studio questions: https://oomol.com

## License

This OOMOL block is open source. The underlying epub-translator library is also open source.

Start exploring literature from around the world in the language that speaks to you - all through a simple visual interface!
