import parseSerials

episodes = parseSerials.load_json("Episodes.json")
counts = []
for episode in episodes:
	counts.append(
		{
			episode["link_name"]:len(episode["episodes"])
		}
	)
for count in counts:
	print(count)
