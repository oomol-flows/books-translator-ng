#region generated meta
import typing
from oocana import LLMModelOptions
class Inputs(typing.TypedDict):
    source_epub: str
    target_language: typing.Literal["English", "Chinese", "Spanish", "French", "German", "Japanese", "Korean", "Portuguese", "Russian", "Italian", "Arabic", "Hindi"]
    submit_mode: typing.Literal["Bilingual (Recommended)", "Single Language", "Bilingual Inline"]
    output_path: str | None
    llm: LLMModelOptions
    custom_prompt: str | None
    max_group_tokens: int | None
    max_retries: int | None
    timeout: float | None
    temperature: float | None
    top_p: float | None
    retry_times: int | None
    retry_interval_seconds: float | None
class Outputs(typing.TypedDict):
    translated_file: typing.NotRequired[str]
    success: typing.NotRequired[bool]
#endregion

from oocana import Context
from pathlib import Path
from epub_translator import LLM, translate, SubmitKind


async def main(params: Inputs, context: Context) -> Outputs:
    """
    Translate an EPUB file to the target language using LLM.

    Args:
        params: Input parameters including source file, target language, and LLM config
        context: OOMOL context for accessing LLM credentials and reporting progress

    Returns:
        Dictionary containing the translated file path and success status
    """
    try:
        # Get LLM configuration with fallback to recommended defaults
        llm_config = params["llm"]

        # Use user-provided values if available, otherwise use recommended defaults
        timeout = params.get("timeout") if params.get("timeout") is not None else 360.0
        temperature = params.get("temperature") if params.get("temperature") is not None else 0.3
        top_p = params.get("top_p") if params.get("top_p") is not None else 0.9
        retry_times = params.get("retry_times") if params.get("retry_times") is not None else 10
        retry_interval = params.get("retry_interval_seconds") if params.get("retry_interval_seconds") is not None else 0.75
        max_retries = params.get("max_retries") if params.get("max_retries") is not None else 10
        max_group_tokens = params.get("max_group_tokens") if params.get("max_group_tokens") is not None else 1200

        # Map user-friendly submit mode to SubmitKind enum
        submit_mode_map = {
            "Bilingual (Recommended)": SubmitKind.APPEND_BLOCK,
            "Single Language": SubmitKind.REPLACE,
            "Bilingual Inline": SubmitKind.APPEND_TEXT
        }
        submit_kind = submit_mode_map[params["submit_mode"]]

        print("v1.0.4 (epub-translator 0.1.4)")
        # Initialize LLM client with OOMOL credentials
        llm = LLM(
            key=await context.oomol_token(),
            url=context.oomol_llm_env.get("base_url_v1"),
            model=llm_config.get("model", "oomol-chat"),
            token_encoding="o200k_base",
            cache_path=None,  # Disable caching
            timeout=timeout,
            temperature=temperature,
            top_p=top_p,
            retry_times=retry_times,
            retry_interval_seconds=retry_interval,
        )

        # Define progress callback
        def on_progress(progress: float):
            """Report translation progress to OOMOL UI"""
            progress_percent = int(progress * 100)
            context.report_progress(progress_percent)

        # Get paths
        source_path = Path(params["source_epub"])

        # Use output_path if provided, otherwise default to session_dir
        if params.get("output_path"):
            output_path = Path(params["output_path"])
        else:
            # Generate output filename based on source and target language
            source_name = source_path.stem
            target_lang = params["target_language"]
            output_filename = f"{source_name}_{target_lang}.epub"
            output_path = Path(context.session_dir) / output_filename

        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Get optional custom prompt
        user_prompt = params.get("custom_prompt")

        # Perform translation
        try:
            translate(
                llm=llm,
                source_path=source_path,
                target_path=output_path,
                target_language=params["target_language"],
                submit=submit_kind,
                user_prompt=user_prompt if user_prompt else None,
                max_retries=max_retries,
                max_group_tokens=max_group_tokens,
                on_progress=on_progress,
            )
        except (ValueError, RuntimeError) as ve:
            error_msg = str(ve)
            if "Element not found in parent" in error_msg:
                # Known issue with epub-translator when using certain submit modes
                # Try fallback to APPEND_BLOCK mode if not already using it
                if submit_kind != SubmitKind.APPEND_BLOCK:
                    print(f"Warning: Encountered XML structure issue with {params['submit_mode']} mode.")
                    print("Retrying with 'Bilingual (Recommended)' mode as fallback...")
                    context.report_progress(0)  # Reset progress for retry

                    try:
                        translate(
                            llm=llm,
                            source_path=source_path,
                            target_path=output_path,
                            target_language=params["target_language"],
                            submit=SubmitKind.APPEND_BLOCK,
                            user_prompt=user_prompt if user_prompt else None,
                            max_retries=max_retries,
                            max_group_tokens=max_group_tokens,
                            on_progress=on_progress,
                        )
                        print("Successfully completed using fallback mode.")
                    except Exception as retry_error:
                        raise RuntimeError(
                            f"Translation failed even with fallback mode due to complex EPUB structure: {str(retry_error)}\n"
                            "This EPUB file has a complex XML structure that the current version of "
                            "epub-translator cannot process correctly. Please try a different EPUB file "
                            "or report this issue to the epub-translator project."
                        )
                else:
                    raise RuntimeError(
                        f"Translation failed due to complex EPUB structure: {error_msg}\n"
                        "This EPUB file has a complex XML structure that the current version of "
                        "epub-translator cannot process correctly. Please try a different EPUB file "
                        "or report this issue to the epub-translator project."
                    )
            else:
                raise

        # Report completion
        context.report_progress(100)

        return {
            "translated_file": str(output_path),
            "success": True
        }

    except Exception as e:
        # Report error and return failure status
        raise RuntimeError(f"Translation failed: {str(e)}")
