### Ensure that code that isn’t part of the prospective commit isn’t tested within your pre-commit script ###
### Stash before the pre-commit command is run ###
# STASH_NAME="pre-commit-$(date +%s)"
# git stash save -q --keep-index $STASH_NAME		# -q = quiet mode


# Command to run before every committed
# repo_root=$( git rev-parse --show-toplevel )
# Move to one above the repo root so git files paths make sense
# cd $repo_root/..
# black --line-length 79 boutique_ado/

### Alternative to run against only the cached files that are about to be committed ##
### Check if there are any commits already ###
### Determines what to run the 'git diff' command against ###
empty_tree=$( git hash-object -t tree /dev/null )

if git rev-parse --verify HEAD > /dev/null 2>&1
then
	against=HEAD
else
	against="$empty_tree"
fi

### Set split so that for loop below can handle spaces in file names by splitting on line breaks
IFS='
'

### Picks every file in the commit ###
for file in $( git diff-index --cached --name-only $against ); do
	### If the file is a Python file ###
	if [[ "$file" == *.py ]]; then
		### Run the 'black' auto-formatter on the file ###
		black --line-length 79 $file
	fi
done


### Pop from stash after the pre-commit command is run ###
# STASHES=$(git stash list)
# if [[ $STASHES == *"$STASH_NAME" ]]; then
# # -q = quiet mode
#   git stash pop -q
# fi


### To install run: ###
# ln -s ../../pre-commit.sh .git/hooks/pre-commit
