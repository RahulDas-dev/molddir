from molddir import Decoder, Encoder, configure_logging


# Create the release Branch:
# git checkout -b release main
# git push origin release

# Merge Changes to release Branch: When you are ready to release:
# git checkout release
# git merge main
# git push origin release

# Run Unit Testing:
# poetry run python -m unittest discover -s tests


def encode_or_decode(encode: bool):
    if encode:
        # code_base_path_ = "/codebase/to/be/encoded/"
        codebase_path_ = "."
        _ = Encoder(codebase_path=codebase_path_)()
    else:
        encoded_file_ = "/your/encoded/file/path"
        output_dir_ = "/the/new/codebase/path"
        Decoder(output_dir=output_dir_)(encoded_file=encoded_file_)


if __name__ == "__main__":
    configure_logging("DEBUG")
    encode_or_decode(encode=True)
